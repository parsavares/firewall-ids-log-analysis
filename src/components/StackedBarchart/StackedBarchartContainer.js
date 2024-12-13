import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import StackedbarchartD3 from './StackedBarchartD3';
import { setStackedBarchartData } from '../../redux/DatasetSlice';
import {formatDate} from '../../utils';

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

    useEffect(()=>{
        const stackedbarchartD3Instance = new StackedbarchartD3(divContainerRef.current);
        stackedbarchartD3Instance.create({size:getCharSize()});
        StackedbarchartD3Ref.current = stackedbarchartD3Instance;

        fetchDataAndUpdate();

        return () => {
            const stackedbarchartD3Instance = StackedbarchartD3Ref.current;
            stackedbarchartD3Instance.clear();
        }
    }, []);

    async function fetchDataAndUpdate(){

        // Fetch the data from server
        const api_endpoint = "getStackedBarchart";
        const xAttribute = "date_time";
        const yAttribute = "syslog_priority";

        const start_date_str = formatDate(state.global_date_time_interval[0])
        const end_date_str = formatDate(state.global_date_time_interval[1])
            
       // const start_date_str = "2011/04/06 17:40:00";
        //const end_date_str = "2020/04/06 20:40:00";

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

        const newState = {
            data: data,
            xAttribute,
            yAttribute
        }

        console.log(newState);
        dispatch(setStackedBarchartData(newState));
    }

    useEffect(()=>{
        divContainerRef.current.style.opacity = 0.5;
        fetchDataAndUpdate();
    }, [state.global_date_time_interval]);
    useEffect(()=>{

        if(state.stackedbarchart_data === null){
            return;
        }   

        divContainerRef.current.style.opacity = 1;
        console.log("state: ", state)
        const data = state.stackedbarchart_data.data;

        const xAttribute = state.stackedbarchart_data.xAttribute;
        const yAttribute = state.stackedbarchart_data.yAttribute;   
        

        StackedbarchartD3Ref.current.clear()
        StackedbarchartD3Ref.current.create({size:getCharSize()});
        StackedbarchartD3Ref.current.render(data, xAttribute, yAttribute);
    }, [state.stackedbarchart_data]);

    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100" >
            <h1>Stackedbarchart</h1>

        </div>
    )

}