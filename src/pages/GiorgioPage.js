
import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import { useSelector } from 'react-redux';

//import ControlBar_ids from '../components/ControlBar/ControlBar_ids';
export default function GiorgioPage() {

    const state = useSelector((state) => state);

    return (
        <div className='h-100 row'>
            <h1>Giorgio</h1>
            <p>
                Giorgio's page
            </p>
            <div className="col-6 h-50">
                <StackedbarchartContainer data_source={"FIREWALL"} yAttribute={"syslog_priority"}/>
            </div>
            <div className="col-6 h-50">
                {/* <StackedbarchartContainer data_source={"IDS"} yAttribute={"priority"}/> */}
                <HeatmapContainer data_source={"FIREWALL"}  yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
            </div>
            <div className="col-6 h-50">
                <StackedbarchartContainer data_source={"FIREWALL"} yAttribute={"cat_src"}/>
            </div>
            <div className="col-6 h-50">
                <StackedbarchartContainer data_source={"FIREWALL"} yAttribute={"destination_service"}/>
            </div>
        </div>
    );
    }
