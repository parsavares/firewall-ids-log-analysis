import React from 'react'  
import { endOfToday, set } from 'date-fns' 
import TimeRange from '@harveyconnor/react-timeline-range-slider'  
import { subDays } from 'date-fns'
import { useDispatch, useSelector } from 'react-redux'

const now = new Date()
const yesterday = subDays(now, 1)

const getTodayAtSpecificHour = (hour = 12) =>
	set(now, { hours: hour, minutes: 0, seconds: 0, milliseconds: 0 })

const getYesterdayAtSpecificHour = (hour = 12) =>
    set(yesterday, { hours: hour, minutes: 0, seconds: 0, milliseconds: 0 })

const selectedStart = getYesterdayAtSpecificHour(0)
const selectedEnd = getTodayAtSpecificHour(14)

const startTime = getTodayAtSpecificHour(0)
const endTime = endOfToday()

class App extends React.Component {  
  state = {  
    error: false,  
    selectedInterval: [selectedStart, selectedEnd],  
  }


    errorHandler = ({ error }) => {}

    onChangeCallback = selectedInterval => {
        console.log(selectedInterval)
        this.setState({ selectedInterval })  
    }

  render() {  
    const { selectedInterval, error } = this.state  
    return (  
      <TimeRange
        error={error}  
        ticksNumber={36}  
        selectedInterval={selectedInterval}  
        timelineInterval={[startTime, endTime]}  
        onUpdateCallback={this.errorHandler}  
        onChangeCallback={this.onChangeCallback}
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
    )  
  }  
}  

export default App