
import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import SankeDiagramContainer from '../components/SankeyDiagram/SankeDiagramContainer';
import TimeControlbar from '../components/TimeControlbar/TimeControlbar';
import { useSelector } from 'react-redux';

//import ControlBar_ids from '../components/ControlBar/ControlBar_ids';
export default function GiorgioPage() {

    const state = useSelector((state) => state);

    return (

        <div className='h-100 row'>
        <h1>FIREWALL Sanke Diagram and Heatmap</h1>
        <div className="row w-100">
            <div className="col-md-6 h-75" style={{flex: '0 0 50%', maxWidth: '50%'}}>
                <SankeDiagramContainer/>
            </div>
            <div className="col-md-6 h-75" style={{flex: '0 0 50%', maxWidth: '50%'}}>
                <HeatmapContainer data_source={"FIREWALL"} yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
            </div>
        </div>
    </div>
    );
}
