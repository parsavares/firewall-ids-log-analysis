import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
//import Papa from "papaparse"

function delete_priorities(item) {
  //arr[index] = item * 10;
  console.log("item.occurrences", item.occurrences)
} 

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
    stackedbarchart_data: null,
    heatmap_data: null,
    parallelsets_data: null,
    heatmap_data_copy: null,
    parallelsets_data_copy: null,
    priority: 'Info',

  },
  reducers: {
    setStackedBarchartData: (state, action) => {
      state.stackedbarchart_data = action.payload;
    },
    setHeatmapData: (state, action) => {
      state.heatmap_data = action.payload
      state.heatmap_data_copy = action.payload
    },
    setParallelsetsData: (state, action) => {
      state.parallelsets_data = action.payload
      state.parallelsets_data_copy = action.payload
    },
    filterPrioritiesParallel: (state, action) => {
      state.parallelsets_data_copy = action.payload
    },
    filterPrioritiesFirewall: (state, action) => {
      //alert(string)
      //console.log('string', string)
      console.log('action.payload', action.payload)
      state.priority = action.payload;
      //state.stackedbarchart_data_copy = {... state.stackedbarchart_data}
      //console.log(state.stackedbarchart_data_copy)
      //state.stackedbarchart_data_copy = 
      //state.stackedbarchart_data_copy.forEach(delete_priorities);
    
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
export const { filterPrioritiesFirewall, filterPrioritiesParallel, setStackedBarchartData, setHeatmapData, setParallelsetsData} = stateSlice.actions

export default stateSlice.reducer