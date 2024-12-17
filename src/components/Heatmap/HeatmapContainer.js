import {useEffect, useRef, useState} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import HeatmapD3 from './HeatmapD3';
import { setHeatmapData } from '../../redux/DatasetSlice';
import {formatDate} from '../../utils';

export default function HeatmapContainer({data_source, xAttribute, yAttribute, priority=null, subnet_bits=24}){

    const redux_state = useSelector(state => state.state);
    const [state, setState] = useState(null);

    const divContainerRef = useRef(null);
    const heatmapD3Ref = useRef(null);

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
        const heatmapD3 = new HeatmapD3(divContainerRef.current);
        heatmapD3.create({size:getCharSize()});
        heatmapD3Ref.current = heatmapD3;
        

        fetchDataAndUpdate()


        return () => {

            const heatmapD3 = heatmapD3Ref.current;
            heatmapD3.clear();
        }
    }, []);

    useEffect(()=>{
        divContainerRef.current.style.opacity = 0.5;
        fetchDataAndUpdate();
    }, [redux_state.global_date_time_interval]);

    useEffect(()=>{ 
        if(state === null){
            return;
        }
        
        divContainerRef.current.style.opacity = 1;

        const data = state.data;
        heatmapD3Ref.current.clear();
        heatmapD3Ref.current.create({size:getCharSize()});
        heatmapD3Ref.current.render(data, state.xAttribute, state.yAttribute);


    }, [state]);

    async function fetchDataAndUpdate(){

        const api_endpoint = "getHeatmap"

        const start_date_str = formatDate(redux_state.global_date_time_interval[0])
        const end_date_str = formatDate(redux_state.global_date_time_interval[1])

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                xAttribute: xAttribute,
                yAttribute: yAttribute,
                start_datetime: start_date_str,
                end_datetime: end_date_str,
                subnet_bits: subnet_bits,
                data_source: data_source,
                priority: priority
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
        setState(newState)
    }


    return (
        <div ref={divContainerRef} className="heatmap-container h-100">
            <h1>HeatmapContainer</h1>
        </div>
    )

}