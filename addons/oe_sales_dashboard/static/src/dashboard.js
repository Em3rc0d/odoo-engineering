/** @odoo-module **/
import { Component, onWillStart, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class OeSalesDashboard extends Component {
    static template = "oe_sales_dashboard.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.state = useState({loading: true, error: "", payload: null});
        onWillStart(() => this.reload());
    }

    async reload() {
        this.state.loading = true;
        this.state.error = "";
        try {
            this.state.payload = await this.orm.call("sale.order", "oe_dashboard_metrics", []);
        } catch (err) {
            this.state.payload = null;
            this.state.error = "Could not load the sales sample; check model rights and server logs.";
        } finally {
            this.state.loading = false;
        }
    }
}
registry.category("actions").add("oe_sales_dashboard.dashboard", OeSalesDashboard);
