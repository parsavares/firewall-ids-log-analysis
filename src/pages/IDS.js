
import HeatmapContainer from '../components/Heatmap/HeatmapContainer';
import StackedbarchartContainer from '../components/StackedBarchart/StackedBarchartContainer';
import { useSelector } from 'react-redux';

export default function IDS() {

    const state = useSelector((state) => state);
    
    return (
        
        <div className='h-100 row'>
            <h1>IDS histograms</h1>

            
            <div className="col-4">

                { <StackedbarchartContainer data_source={"IDS"} yAttribute={"priority"}/> }
            </div>
            <div className="col-4">
            {<StackedbarchartContainer data_source={"IDS"} yAttribute={"cat_src"}/>}

            </div>
            <div className="col-4 ">

                {<StackedbarchartContainer data_source={"IDS"} yAttribute={"cat_dst"}/>} 
            </div>
            {/*
            <div className="col-md-3 h-50" style={{flex: '0 0 50.00%', maxWidth: '33.333%'}}>
                <SankeDiagramContainer/>
            </div>
            <div className="col-md-3 h-50" style={{flex: '0 0 50.00%', maxWidth: '33.333%'}}>
                <HeatmapContainer data_source={"FIREWALL"}  yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
            </div>
            <div className="col-6">
                    <SankeDiagramContainer/>
                </div>

            <div className="col-md-4 h-50" style={{flex: '0 0 33.333%', maxWidth: '33.333%'}}>
                { <StackedbarchartContainer data_source={"IDS"} yAttribute={"priority"}/> }
                <HeatmapContainer data_source={"FIREWALL"}  yAttribute={"cat_src"} xAttribute={"destination_ip"} subnet_bits={24}/>
            </div>

            */}
        </div>
    
    )}
                
        
    