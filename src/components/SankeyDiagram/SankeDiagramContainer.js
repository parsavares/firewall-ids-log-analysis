import {useState, useEffect, useRef} from 'react';
import {useSelector, useDispatch} from 'react-redux';
import {formatDate} from '../../utils';
import SankeDiagramD3 from './SankeDiagramD3';
import { setSankeDiagramData } from '../../redux/DatasetSlice';

export default function SankeDiagramContainer(){

    const redux_state = useSelector(state => state.state);

    const [state, setState] = useState(null);

    // ContorlBar state
    //const [uniqueFilterValues, setUniqueFilterVariables] = useState([]);
    //const [activeValues, setActiveValues] = useState([])

    const divContainerRef = useRef(null);
    const SankeDiagramD3Ref = useRef(null);

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
        const SankeDiagramD3Instance = new SankeDiagramD3(divContainerRef.current);

        SankeDiagramD3Instance.create({size:getCharSize()});
        SankeDiagramD3Ref.current = SankeDiagramD3Instance;

        fetchDataAndUpdate();

        return () => {
            const SankeDiagramD3Instance = SankeDiagramD3Ref.current;
            SankeDiagramD3Instance.clear();
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

        /*
        // Check if already done
        if(uniqueFilterValues.length === 0){
            const values = Object.keys(state);
            setUniqueFilterVariables(values);
            setActiveValues(values)
        }*/

        console.log('SankeDiagramContainer state:', state);
        divContainerRef.current.style.opacity = 1;
        const data = state;
        SankeDiagramD3Ref.current.clear();
        SankeDiagramD3Ref.current.create({size:getCharSize()});
        SankeDiagramD3Ref.current.render(data);

    }, [state]);

    async function fetchDataAndUpdate(){
        const api_endpoint = "getSankeDiagram";

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

        setState((data));

    }


    return (
        <div ref={divContainerRef} className="Stackedbarchart-container h-100">
            <h1>SankeDiagramContainer</h1>

        </div>
    )

}