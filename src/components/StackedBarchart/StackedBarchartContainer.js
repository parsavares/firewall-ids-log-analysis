import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import StackedbarchartD3 from './StackedBarchartD3';
import { setStackedBarchartData } from '../../redux/DatasetSlice';

export default function StackedbarchartContainer(){

    const state = useSelector(state => state.state);
    const dispatch = useDispatch();

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
        console.log(priority);
        data = data.map(obj => {
            // Copy the occurrences object
            const newOccurrences = { ...obj.occurrences };
    
            // Update all keys except the priority to have a value of 0
            Object.keys(newOccurrences).forEach(key => {
                if (key !== priority) {
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


        // Fetch the data from server
        const api_endpoint = "debug";
        const xAttribute = "date_time";
        const yAttribute = "syslog_priority";

        const start_date_str = "2011/04/06 17:40:00";
        const end_date_str = "2020/04/06 20:40:00";

        fetchData(api_endpoint, xAttribute, yAttribute, start_date_str, end_date_str).then(data => {

            const newState = {
                data: data,
                xAttribute,
                yAttribute
            }

            console.log(newState);
            dispatch(setStackedBarchartData(newState));
        });

        return () => {
            const stackedbarchartD3Instance = StackedbarchartD3Ref.current;
            stackedbarchartD3Instance.clear();
        }
    }, []);

    async function fetchData(api_endpoint, xAttribute, yAttribute, start_date_str, end_date_str){

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                xAttribute: xAttribute,
                yAttribute: yAttribute,
                start_datetime: start_date_str,
                end_datetime: end_date_str
            }
        
        const queryString = new URLSearchParams(params).toString();
        const url = `${baseUrl}?${queryString}`;
        const response = await fetch(url);
        const data = await response.json();

        return data;
    }

    useEffect(()=>{

        if(state.stackedbarchart_data === null){
            return;
        }
        
        console.log("before", state.stackedbarchart_data.data)

        const data = delete_priorities(state.stackedbarchart_data.data, state.priority)
        const xAttribute = state.stackedbarchart_data.xAttribute;
        const yAttribute = state.stackedbarchart_data.yAttribute;

        
        console.log("updated", data)
        StackedbarchartD3Ref.current.render(data, xAttribute, yAttribute);
    }, [state, dispatch]);

    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100">
            <h1>Stackedbarchart</h1>

        </div>
    )

}