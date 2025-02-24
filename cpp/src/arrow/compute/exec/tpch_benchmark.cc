// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

#include <benchmark/benchmark.h>

#include "arrow/compute/cast.h"
#include "arrow/compute/exec/options.h"
#include "arrow/compute/exec/test_util.h"
#include "arrow/compute/exec/tpch_node.h"
#include "arrow/testing/future_util.h"
#include "arrow/util/make_unique.h"

namespace arrow {
namespace compute {
namespace internal {

std::shared_ptr<ExecPlan> Plan_Q1(AsyncGenerator<util::optional<ExecBatch>>* sink_gen,
                                  int scale_factor) {
  ExecContext* ctx = default_exec_context();
  *ctx = ExecContext(default_memory_pool(), arrow::internal::GetCpuThreadPool());
  std::shared_ptr<ExecPlan> plan = *ExecPlan::Make(ctx);
  std::unique_ptr<TpchGen> gen =
      *TpchGen::Make(plan.get(), static_cast<double>(scale_factor));

  ExecNode* lineitem =
      *gen->Lineitem({"L_QUANTITY", "L_EXTENDEDPRICE", "L_TAX", "L_DISCOUNT",
                      "L_SHIPDATE", "L_RETURNFLAG", "L_LINESTATUS"});

  auto sept_2_1998 = std::make_shared<Date32Scalar>(
      10471);  // September 2, 1998 is 10471 days after January 1, 1970
  Expression filter =
      less_equal(field_ref("L_SHIPDATE"), literal(std::move(sept_2_1998)));
  FilterNodeOptions filter_opts(filter);

  Expression l_returnflag = field_ref("L_RETURNFLAG");
  Expression l_linestatus = field_ref("L_LINESTATUS");
  Expression quantity = field_ref("L_QUANTITY");
  Expression base_price = field_ref("L_EXTENDEDPRICE");

  std::shared_ptr<Decimal128Scalar> decimal_1 =
      std::make_shared<Decimal128Scalar>(Decimal128{0, 100}, decimal(12, 2));
  Expression discount_multiplier =
      call("subtract", {literal(decimal_1), field_ref("L_DISCOUNT")});
  Expression tax_multiplier = call("add", {literal(decimal_1), field_ref("L_TAX")});
  Expression disc_price =
      call("multiply", {field_ref("L_EXTENDEDPRICE"), discount_multiplier});
  Expression charge =
      call("multiply",
           {call("cast",
                 {call("multiply", {field_ref("L_EXTENDEDPRICE"), discount_multiplier})},
                 compute::CastOptions::Unsafe(decimal(12, 2))),
            tax_multiplier});
  Expression discount = field_ref("L_DISCOUNT");

  std::vector<Expression> projection_list = {l_returnflag, l_linestatus, quantity,
                                             base_price,   disc_price,   charge,
                                             quantity,     base_price,   discount};
  std::vector<std::string> project_names = {
      "l_returnflag", "l_linestatus", "sum_qty",   "sum_base_price", "sum_disc_price",
      "sum_charge",   "avg_qty",      "avg_price", "avg_disc"};
  ProjectNodeOptions project_opts(std::move(projection_list), std::move(project_names));

  auto sum_opts =
      std::make_shared<ScalarAggregateOptions>(ScalarAggregateOptions::Defaults());
  auto count_opts = std::make_shared<CountOptions>(CountOptions::CountMode::ALL);
  std::vector<arrow::compute::internal::Aggregate> aggs = {
      {"hash_sum", sum_opts},  {"hash_sum", sum_opts},    {"hash_sum", sum_opts},
      {"hash_sum", sum_opts},  {"hash_mean", sum_opts},   {"hash_mean", sum_opts},
      {"hash_mean", sum_opts}, {"hash_count", count_opts}};

  std::vector<FieldRef> to_aggregate = {"sum_qty",    "sum_base_price", "sum_disc_price",
                                        "sum_charge", "avg_qty",        "avg_price",
                                        "avg_disc",   "sum_qty"};

  std::vector<std::string> names = {"sum_qty",    "sum_base_price", "sum_disc_price",
                                    "sum_charge", "avg_qty",        "avg_price",
                                    "avg_disc",   "count_order"};

  std::vector<FieldRef> keys = {"l_returnflag", "l_linestatus"};
  AggregateNodeOptions agg_opts(aggs, to_aggregate, names, keys);

  SortKey l_returnflag_key("l_returnflag");
  SortKey l_linestatus_key("l_linestatus");
  SortOptions sort_opts({l_returnflag_key, l_linestatus_key});
  OrderBySinkNodeOptions order_by_opts(sort_opts, sink_gen);

  Declaration filter_decl("filter", {Declaration::Input(lineitem)}, filter_opts);
  Declaration project_decl("project", project_opts);
  Declaration aggregate_decl("aggregate", agg_opts);
  Declaration orderby_decl("order_by_sink", order_by_opts);

  Declaration q1 =
      Declaration::Sequence({filter_decl, project_decl, aggregate_decl, orderby_decl});
  std::ignore = *q1.AddToPlan(plan.get());
  return plan;
}

static void BM_Tpch_Q1(benchmark::State& st) {
  for (auto _ : st) {
    st.PauseTiming();
    AsyncGenerator<util::optional<ExecBatch>> sink_gen;
    std::shared_ptr<ExecPlan> plan = Plan_Q1(&sink_gen, static_cast<int>(st.range(0)));
    st.ResumeTiming();
    auto fut = StartAndCollect(plan.get(), sink_gen);
    auto res = *fut.MoveResult();
  }
}

BENCHMARK(BM_Tpch_Q1)->Args({1})->ArgNames({"ScaleFactor"});
}  // namespace internal
}  // namespace compute
}  // namespace arrow
