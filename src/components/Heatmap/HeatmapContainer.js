import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import HeatmapD3 from './HeatmapD3';
import { setHeatmapData } from '../../redux/DatasetSlice';

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
        
        const api_endpoint = "getHeatmap"
        //const xAttribute = "cat_dst";
        //const yAttribute = "cat_src";
        const xAttribute = "source_ip";
        const yAttribute = "destination_ip";

        const start_date_str = "2011/04/06 17:40:00";
        const end_date_str = "2020/04/06 20:40:00";


        fetchData(api_endpoint, xAttribute, yAttribute, start_date_str, end_date_str, 24).then(data => {
            const newState = {
                data: data,
                xAttribute,
                yAttribute
            }
            dispatch(setHeatmapData(newState));
        });

        return () => {

            const heatmapD3 = heatmapD3Ref.current;
            heatmapD3.clear();
        }
    }, []);

    async function fetchData(api_endpoint, xAttribute, yAttribute, start_date_str, end_date_str, subnet_bits){

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

        return data;
    }

    useEffect(()=>{
        if(state.heatmap_data === null){
            return;
        }

        const data = state.heatmap_data.data;
        const keys = Object.keys(data[0]);
        heatmapD3Ref.current.render(data, keys[0], keys[1]);

    }, [state, dispatch]);

    return (
        <div ref={divContainerRef} className="heatmap-container h-100">
            <h1>Heatmap</h1>

        </div>
    )

}