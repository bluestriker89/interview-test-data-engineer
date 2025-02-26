# Copyright 2018-2019 QuantumBlack Visual Analytics Limited
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND
# NONINFRINGEMENT. IN NO EVENT WILL THE LICENSOR OR OTHER CONTRIBUTORS
# BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# The QuantumBlack Visual Analytics Limited (“QuantumBlack”) name and logo
# (either separately or in combination, “QuantumBlack Trademarks”) are
# trademarks of QuantumBlack. The License does not grant you any right or
# license to the QuantumBlack Trademarks. You may not use the QuantumBlack
# Trademarks or any confusingly similar mark as a trademark for your product,
#     or use the QuantumBlack Trademarks in any other manner that might cause
# confusion in the marketplace, including but not limited to in advertising,
# on websites, or on software.
#
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pipeline construction."""

from kedro.pipeline import Pipeline, node

from .nodes.de_ingest import (
ingest_customer,
ingest_lineitem,
ingest_nation,
ingest_orders,
ingest_part,
ingest_partsupp,
ingest_region,
ingest_supplier,
)
from .nodes.de_sc_data_model import (
customer_dimension,
part_dimension,
supplier_dimension,
order_fact,
)

# Here you can define your data-driven pipeline by importing your functions
# and adding them to the pipeline as follows:
#
# from nodes.data_wrangling import clean_data, compute_features
#
# pipeline = Pipeline([
#     node(clean_data, 'customers', 'prepared_customers'),
#     node(compute_features, 'prepared_customers', ['X_train', 'Y_train'])
# ])
#
# Once you have your pipeline defined, you can run it from the root of your
# project by calling:
#
# $ kedro run
#


def create_pipeline(**kwargs):
    """Create the project's pipeline.

    Args:
        kwargs: Ignore any additional arguments added in the future.

    Returns:
        Pipeline: The resulting pipeline.

    """


    ###########################################################################
    # Here you can find an example pipeline with 4 nodes.
    #
    # PLEASE DELETE THIS PIPELINE ONCE YOU START WORKING ON YOUR OWN PROJECT AS
    # WELL AS THE FILE nodes/example.py
    # -------------------------------------------------------------------------

    de_ingest = Pipeline(
        [
            node(ingest_customer, "raw_customer", "prim_customer"),
            node(ingest_lineitem, "raw_lineitem", "prim_lineitem"),
            node(ingest_nation, "raw_nation", "prim_nation"),
            node(ingest_orders, "raw_orders", "prim_orders"),
            node(ingest_part, "raw_part", "prim_part"),
            node(ingest_partsupp, "raw_partsupp", "prim_partsupp"),
            node(ingest_region, "raw_region", "prim_region"),
            node(ingest_supplier, "raw_supplier", "prim_supplier")
        ]
    )
    de_star_schema = Pipeline(
        [
            node(customer_dimension,
                 [
                     "prim_customer",
                     "prim_region",
                     "prim_nation"
                 ],
                 "customer_dimension"),
            node(part_dimension, "prim_part", "part_dimension"),
            node(supplier_dimension,
                 [
                     "prim_supplier",
                     "prim_region",
                     "prim_nation"
                 ],
                 "supplier_dimension"),
            node(order_fact,
                 [
                     "prim_orders",
                     "prim_lineitem",
                     "prim_partsupp"
                 ],
                 "order_fact"),
        ]
    )

    return de_ingest + de_star_schema
