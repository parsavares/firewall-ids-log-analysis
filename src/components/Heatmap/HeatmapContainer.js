import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';

import HeatmapD3 from './HeatmapD3';

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
        return () => {
            const heatmapD3 = heatmapD3Ref.current;
            heatmapD3.clear();
        }
    }, []);

    async function fetchData(){
        const response = await fetch('http://localhost:5000/getHeatmap');
        const data = await response.json();

        return data;
    }

    useEffect(()=>{
        const heatmapD3 = heatmapD3Ref.current;


        fetchData().then(data => {
            const keys = Object.keys(data[0]);
            heatmapD3.render(data, keys[0], keys[1]);
        });

    }, [state, dispatch]);

    return (
        <div ref={divContainerRef} className="heatmap-container h-100">
            <h1>Heatmap</h1>

        </div>
    )

}