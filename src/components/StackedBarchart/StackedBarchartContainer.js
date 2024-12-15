import {act, useEffect, useRef, useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import StackedbarchartD3 from './StackedBarchartD3';
import { setStackedBarchartData } from '../../redux/DatasetSlice';
import {formatDate} from '../../utils';
import {setFilterPrioritiesFirewall} from '../../redux/DatasetSlice';
import ControlBar from '../ControlBar/ControlBar';
import * as d3 from 'd3';

export default function StackedbarchartContainer({data_source, yAttribute}){

    // Redux state
    const redux_state = useSelector(state => state.state);
    
    const [state, setState] = useState(null);

    // ContorlBar state
    const [uniqueFilterValues, setUniqueFilterVariables] = useState([]);
    const [activeValues, setActiveValues] = useState([])


    const divContainerRef = useRef(null);
    const StackedbarchartD3Ref = useRef(null);

    const getCharSize = function(){
        let width;
        let height;
        if(divContainerRef.current!==undefined){
            width=divContainerRef.current.offsetWidth;
            height=divContainerRef.current.offsetHeight;
        }
        return {width:width, height:height};
    }

    const delete_priorities = function(data, priority) {
        data = data.map(obj => {
            // Copy the occurrences object
            const newOccurrences = { ...obj.occurrences };
    
            // Update all keys except the priority to have a value of 0
            Object.keys(newOccurrences).forEach(key => {
                if (!priority.includes(key)) {
                    newOccurrences[key] = 0;
                }
            });
    
            // Return the updated object
            return {
                interval_center: obj.interval_center,
                total_occurrences: obj.total_occurrences,
                occurrences: newOccurrences
            };
        });
        return data;
    };

    useEffect(()=>{
        const stackedbarchartD3Instance = new StackedbarchartD3(divContainerRef.current);

        stackedbarchartD3Instance.create({size:getCharSize()});
        StackedbarchartD3Ref.current = stackedbarchartD3Instance;


        fetchDataAndUpdate()

        
        return () => {
            const stackedbarchartD3Instance = StackedbarchartD3Ref.current;
            stackedbarchartD3Instance.clear();
        }
    }, []);

    async function fetchDataAndUpdate(){

        // Fetch the data from server
        const api_endpoint = "getStackedBarchart";
        const xAttribute = "date_time";

        const start_date_str = formatDate(redux_state.global_date_time_interval[0])
        const end_date_str = formatDate(redux_state.global_date_time_interval[1])
            
       // const start_date_str = "2011/04/06 17:40:00";
        //const end_date_str = "2020/04/06 20:40:00";

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                xAttribute: xAttribute,
                yAttribute: yAttribute,
                start_datetime: start_date_str,
                end_datetime: end_date_str,
                data_source: data_source
            }
        
        const queryString = new URLSearchParams(params).toString();
        const url = `${baseUrl}?${queryString}`;
        const response = await fetch(url);
        const data = await response.json();

        const newState = {
            data,
            xAttribute,
            yAttribute
        }

        setState(newState);
    }

    useEffect(()=>{

        divContainerRef.current.style.opacity = 0.5;
        fetchDataAndUpdate();

    }, [redux_state.global_date_time_interval]);

    useEffect(()=>{
        /*
        if(state.stackedbarchart_data === null){
            return;
        }*/
       if(state === null){
           return;
       } 

        // Check if already done
        if(uniqueFilterValues.length === 0){
            //const values = Object.keys(state.stackedbarchart_data.data[0].occurrences);
            const values = Object.keys(state.data[0].occurrences);
            setUniqueFilterVariables(values);
            setActiveValues(values)
        }

        const filtered = delete_priorities(state.data, activeValues)
        const xAttribute = state.data.xAttribute;
        const yAttribute = state.data.yAttribute;

        divContainerRef.current.style.opacity = 1;
        StackedbarchartD3Ref.current.render(filtered, xAttribute, yAttribute);
        
    }, [state, activeValues]);

    return (
        <div className='h-100'>
            <div className='h-20'>
                {
                    uniqueFilterValues.length > 0 ? <ControlBar labelsList={uniqueFilterValues} activeLabels={activeValues} setActiveLabels={setActiveValues}/>
                    : null
                }
            </div>
            <div ref={divContainerRef} className="Stackedbarchart-container h-100" >
                <h1>Stackedbarchart</h1>
            </div>
        </div>
   )

}