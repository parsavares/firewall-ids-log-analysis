
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import StackedbarchartContainer_ids from '../components/StackedBarchart/StackedBarchartContainer_ids';
import ControlBar from '../components/ControlBar/ControlBar';
//import ControlBar_ids from '../components/ControlBar/ControlBar_ids';
export default function GiorgioPage() {
    return (
        <div className='h-100'>
        <h1>Giorgio</h1>
        <p>
            Giorgio's page
        </p>
        <ControlBar/>
        <StackedbarchartContainer/>
        </div>
    );
    }
    