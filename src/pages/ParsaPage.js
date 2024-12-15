import HeatmapContainer from "../components/Heatmap/HeatmapContainer";

export default function ParsaPage() {
    return (
        <div className="row h-100">
            <div className="col-3">
                <HeatmapContainer data_source={"FIREWALL"} xAttribute={"cat_src"} yAttribute={"syslog_priority"}/>
            </div>
            <div className="col-3">
                <HeatmapContainer data_source={"FIREWALL"} xAttribute={"cat_dst"} yAttribute={"syslog_priority"}/>
            </div>
            <div className="col-3">
                <HeatmapContainer data_source={"FIREWALL"} xAttribute={"message_code"} yAttribute={"syslog_priority"}/>
            </div>
            <div className="col-3">
                <HeatmapContainer data_source={"FIREWALL"} xAttribute={"operation"} yAttribute={"syslog_priority"}/>
            </div>
        </div>
    );
    }
    