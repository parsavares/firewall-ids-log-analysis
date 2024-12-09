import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';

export default function FerraPage() {
    return (
        <div className='h-100'>
            <h1>Ferra</h1>
            <HeatmapContainer />
            <StackedbarchartContainer />
        </div>
    );
    }
    