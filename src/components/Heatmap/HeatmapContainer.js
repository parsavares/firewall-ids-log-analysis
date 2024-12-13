import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import HeatmapD3 from './HeatmapD3';
import { setHeatmapData } from '../../redux/DatasetSlice';
import {formatDate} from '../../utils';

export default function HeatmapContainer(){

    const state = useSelector(state => state.state);
    const dispatch = useDispatch();

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
    }, [state.global_date_time_interval]);

    useEffect(()=>{ 
        if(state.heatmap_data === null){
            return;
        }
        
        divContainerRef.current.style.opacity = 1;

        const data = state.heatmap_data.data;
        const keys = Object.keys(data[0]);
        heatmapD3Ref.current.clear();
        heatmapD3Ref.current.create({size:getCharSize()});
        heatmapD3Ref.current.render(data, keys[0], keys[1]);


    }, [state.heatmap_data]);

    async function fetchDataAndUpdate(){

        const api_endpoint = "getHeatmap"
        //const xAttribute = "cat_dst";
        //const yAttribute = "cat_src";
        const xAttribute = "source_ip";
        const yAttribute = "destination_ip";

        const start_date_str = formatDate(state.global_date_time_interval[0])
        const end_date_str = formatDate(state.global_date_time_interval[1])
        const subnet_bits = 24;

        const baseUrl = `http://localhost:5000/${api_endpoint}`;
        const params = 
            {
                xAttribute: xAttribute,
                yAttribute: yAttribute,
                start_datetime: start_date_str,
                end_datetime: end_date_str,
                subnet_bits: subnet_bits
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
        dispatch(setHeatmapData(newState));
    }


    return (
        <div ref={divContainerRef} className="heatmap-container h-100">

        </div>
    )

}