import React, {useState} from 'react'  
import { endOfToday, set } from 'date-fns' 
import TimeRange from '@harveyconnor/react-timeline-range-slider'  
import { subDays } from 'date-fns'
import { useDispatch, useSelector } from 'react-redux'
import { setGlobalDateTimeInterval } from '../../redux/DatasetSlice'

function App() {  

    const startDate = new Date(2012, 3, 5, 0, 0, 0)
    const endDate = new Date(2012, 3, 7, 0, 0, 0)

    const [state, setState] = useState({  
        error: false,  
        selectedInterval: [startDate, endDate],  
    })

    const redux_state = useSelector(state => state.state)
    const dispatch = useDispatch()


    const errorHandler = ({ error }) => {}

    const onChangeCallback = selectedInterval => {
        dispatch(setGlobalDateTimeInterval(selectedInterval))
        console.log(selectedInterval)
        setState(prevState => ({ ...prevState, selectedInterval }))  
        
    }



    return (
        <div className="w-100">
            <div className='mb-5'>
                <TimeRange
                    error={state.error}
                    ticksNumber={36}
                    selectedInterval={state.selectedInterval}
                    timelineInterval={[startDate, endDate]}
                    onUpdateCallback={errorHandler}
                    onChangeCallback={onChangeCallback}
                    formatTick={ms => {
                        const date = new Date(ms);
                        const year = date.getFullYear();
                        const month = date.getMonth() + 1; // Months are zero-indexed
                        const day = date.getDate();
                        const hours = date.getHours();
                        const minutes = date.getMinutes();
                        return `${year}-${month < 10 ? '0' : ''}${month}-${day < 10 ? '0' : ''}${day} ${hours}:${minutes < 10 ? '0' : ''}${minutes}`;
                    }}
                    trackStyles={{
                        valid: {
                            backgroundColor: 'rgba(98, 203, 102, 0.5)',
                            borderLeft: '1px solid #62CB66',
                            borderRight: '1px solid #62CB66',
                        }
                    }}
                    handleColors={{
                        valid: 'rgb(98, 203, 102)'
                    }}
                />
            </div>
            <div className="d-flex justify-content-center">
                {state.selectedInterval[0].toLocaleString()} - {state.selectedInterval[1].toLocaleString()}
            </div>
        </div>
    )
    
}  

export default App