import {useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';


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

    return (
        <div ref={divContainerRef} className="heatmap-container h-100">
            <h1>Heatmap</h1>
        </div>
    )

}