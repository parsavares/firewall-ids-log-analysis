import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
import { set } from 'date-fns'
//import Papa from "papaparse"

// get the data in asyncThunk
export const fetchFileData = createAsyncThunk('seoulBikeData/fetchData', async () => {
  /*
    const response = await fetch('data/SeoulBikeData.csv');
    const responseText = await response.text();
    console.log("loaded file length:" + responseText.length);
    //onst responseJson = Papa.parse(responseText,{header:true, dynamicTyping:true});
    //return responseJson.data.map((item,i)=>{return {...item,index:i}}).slice(0, -7000); // 
    //return responseJson.data.map((item,i)=>{return {...item,index:i}}).slice(0, 10); // 
    return responseJson.data.map((item,i)=>{return {...item,index:i}});
    // when a result is returned, extraReducer below is triggered with the case setSeoulBikeData.fulfilled
    */

    return {}
})


export const stateSlice = createSlice({
  name: 'state',
  initialState: {
    global_date_time_interval: [],
    stackedbarchart_data: null,
    heatmap_data: null,
    parallelsets_data: null
  },
  reducers: {
    setGlobalDateTimeInterval: (state, action) => {
      state.global_date_time_interval = action.payload;
    },
    setStackedBarchartData: (state, action) => {
      state.stackedbarchart_data = action.payload;
    },
    setHeatmapData: (state, action) => {
      state.heatmap_data = action.payload
    },
    setParallelsetsData: (state, action) => {
      state.parallelsets_data = action.payload
    }

  },
  /*
  extraReducers: builder => {
    builder.addCase(fetchFileData.fulfilled, (state, action) => {
      // Add any fetched house to the array
      return prepareInitialState(action.payload)
    })
  }
    */
})

// Action creators are generated for each case reducer function
export const { setStackedBarchartData, setHeatmapData, setParallelsetsData} = stateSlice.actions

export default stateSlice.reducer