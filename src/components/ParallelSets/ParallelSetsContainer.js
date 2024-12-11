import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import ParallelSetsD3 from './ParallelSetsD3';

export default function ParallelSetsContainer(){

    const state = useSelector(state => state.state);
    const dispatch = useDispatch();

    const divContainerRef = useRef(null);
    const ParallelSetsD3Ref = useRef(null);

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
        const ParallelSetsD3Instance = new ParallelSetsD3(divContainerRef.current);
        ParallelSetsD3Instance.create({size:getCharSize()});
        ParallelSetsD3Ref.current = ParallelSetsD3Instance;
        return () => {
            const ParallelSetsD3Instance = ParallelSetsD3Ref.current;
            ParallelSetsD3Instance.clear();
        }
    }, []);

    async function fetchData(api_endpoint, start_date_str, end_date_str, subnet_bits){

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                start_datetime: start_date_str,
                end_datetime: end_date_str,
                subnet_bits
            }
        
        const queryString = new URLSearchParams(params).toString();
        const url = `${baseUrl}?${queryString}`;
        const response = await fetch(url);
        const data = await response.json();

        return data;
    }

    useEffect(()=>{
        const ParallelSetsD3 = ParallelSetsD3Ref.current;

        const api_endpoint = "getParallelSets";

        const start_date_str = "2011/04/06 17:40:00";
        const end_date_str = "2020/04/06 20:40:00";
        const subnet_bits = 24;
        fetchData(api_endpoint, start_date_str, end_date_str, subnet_bits).then(data => {
            alert("Fetched")
            ParallelSetsD3.render(data);
        });

    }, [state, dispatch]);

    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100">
            <h1>ParallelSetsContainer</h1>

        </div>
    )

}