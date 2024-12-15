import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import ParallelSetsContainer from '../components/ParallelSets/ParallelSetsContainer';
import TimeControlbar from '../components/TimeControlbar/TimeControlbar';
import SankeDiagramContainer from '../components/SankeyDiagram/SankeDiagramContainer';
export default function FerraPage() {
    return (
        <div className='h-100'>
            <h1>Ferra</h1>
            {/*<HeatmapContainer />*/}
            <div className="row h-50">
                <div className="col-6">
                    {/* <StackedbarchartContainer /> */}
                </div>
                <div className="col-6">
                    <HeatmapContainer data_source={"FIREWALL"}  yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
                </div>
            </div>
            <div className="row h-50">
                <div className="col-6">
                    <ParallelSetsContainer/>
                </div>
                <div className="col-6">
                    <SankeDiagramContainer/>
                </div>
            </div>
        </div>
    );
    }
    