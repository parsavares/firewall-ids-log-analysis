import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import ParallelSetsContainer from '../components/ParallelSets/ParallelSetsContainer';

export default function FerraPage() {
    return (
        <div className='h-100'>
            <h1>Ferra</h1>
            {/*<HeatmapContainer />*/}
            <ParallelSetsContainer/>
        </div>
    );
    }
    