import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import ParallelSetsContainer from '../components/ParallelSets/ParallelSetsContainer';
import TimeControlbar from '../components/TimeControlbar/TimeControlbar';
import SankeDiagramContainer from '../components/SankeyDiagram/SankeDiagramContainer';
export default function FerraPage() {
    return (
        <div className='h-75 row'>
    <h1>FIREWALL Sanke Diagram and Heatmap</h1>
    <div className="row w-100">
        <div className="col-md-6 h-50" style={{flex: '0 0 50%', maxWidth: '50%'}}>
            <SankeDiagramContainer/>
        </div>
        <div className="col-md-6 h-50" style={{flex: '0 0 50%', maxWidth: '50%'}}>
            <HeatmapContainer data_source={"FIREWALL"} yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
        </div>
    </div>
</div>
    );
    }
    