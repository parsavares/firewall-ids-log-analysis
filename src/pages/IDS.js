
import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import { useSelector } from 'react-redux';

export default function IDS() {

    const state = useSelector((state) => state);
    
    return (
        
        <div class='h-75 row'>
            <h1>IDS</h1>
            <div className="col-md-4 h-50" style={{flex: '0 0 33.333%', maxWidth: '33.333%'}}>
                Select types of priorities
                {<StackedbarchartContainer data_source={"IDS"} yAttribute={"priority"}/>}
            </div>
            <div className="col-md-4 h-50" style={{flex: '0 0 33.333%', maxWidth: '33.333%'}}>
                Select category for the source IP
                {<StackedbarchartContainer data_source={"IDS"} yAttribute={"cat_src"}/>}
            </div>
            <div className="col-md-4 h-50" style={{flex: '0 0 33.333%', maxWidth: '33.333%'}}>
                elect category for the destination IP
                {<StackedbarchartContainer data_source={"IDS"} yAttribute={"cat_dst"}/>}
            </div>
        </div>
    
    )}
                
        
    