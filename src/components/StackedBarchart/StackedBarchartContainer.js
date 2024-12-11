import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import StackedbarchartD3 from './StackedBarchartD3';

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
        const StackedbarchartD3 = StackedbarchartD3Ref.current;

        const api_endpoint = "getStackedBarchart";
        const xAttribute = "date_time";
        const yAttribute = "syslog_priority";

        const start_date_str = "2011/04/06 17:40:00";
        const end_date_str = "2020/04/06 20:40:00";

        fetchData(api_endpoint, xAttribute, yAttribute, start_date_str, end_date_str).then(data => {
            const keys = Object.keys(data[0]);
            StackedbarchartD3.render(data, keys[0], keys[1]);
            
        });

    }, [state, dispatch]);

    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100">
            <h1>Stackedbarchart</h1>

        </div>
    )

}