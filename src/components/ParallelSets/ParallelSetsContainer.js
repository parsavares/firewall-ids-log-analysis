import {useState, useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {formatDate} from '../../utils';
import ParallelSetsD3 from './ParallelSetsD3';
import { setParallelsetsData } from '../../redux/DatasetSlice';

export default function ParallelSetsContainer(){

    const redux_state = useSelector(state => state.state);
    const [state, setState] = useState(null);
    

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

        fetchDataAndUpdate();
        return () => {
            const ParallelSetsD3Instance = ParallelSetsD3Ref.current;
            ParallelSetsD3Instance.clear();
        }
    }, []);


    useEffect(()=>{
        divContainerRef.current.style.opacity = 0.5;
        fetchDataAndUpdate();
    }, [redux_state.global_date_time_interval]);

    useEffect(()=>{
        if(state===null)
            return;

        divContainerRef.current.style.opacity = 1;
        const data = state;
        
        console.log(data);
        ParallelSetsD3Ref.current.clear();
        ParallelSetsD3Ref.current.create({size:getCharSize()});
        ParallelSetsD3Ref.current.render(data);
    }, [state]);

    async function fetchDataAndUpdate(){
        const api_endpoint = "getParallelSets";

        const start_date_str = formatDate(redux_state.global_date_time_interval[0])
        const end_date_str = formatDate(redux_state.global_date_time_interval[1])
        const subnet_bits = 24;
        const data_source = "FIREWALL"

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                start_datetime: start_date_str,
                end_datetime: end_date_str,
                subnet_bits,
                data_source
            }
        
        const queryString = new URLSearchParams(params).toString();
        const url = `${baseUrl}?${queryString}`;
        const response = await fetch(url);
        const data = await response.json();


        setState(data);

    }


    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100">
            <h1>ParallelSetsContainer</h1>

        </div>
    )

}