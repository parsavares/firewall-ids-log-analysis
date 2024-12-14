import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'


/*
// get the data in asyncThunk
export const fetchFileData = createAsyncThunk('seoulBikeData/fetchData', async () => {
  
    const response = await fetch('data/SeoulBikeData.csv');
    const responseText = await response.text();
    console.log("loaded file length:" + responseText.length);
    //onst responseJson = Papa.parse(responseText,{header:true, dynamicTyping:true});
    //return responseJson.data.map((item,i)=>{return {...item,index:i}}).slice(0, -7000); // 
    //return responseJson.data.map((item,i)=>{return {...item,index:i}}).slice(0, 10); // 
    return responseJson.data.map((item,i)=>{return {...item,index:i}});
    // when a result is returned, extraReducer below is triggered with the case setSeoulBikeData.fulfilled
    

    return {}
})
*/

export const stateSlice = createSlice({
  name: 'state',
  initialState: {
    stackedbarchart_data: null,
    stackedbarchart_data_ids: null,
    heatmap_data: null,
    parallelsets_data: null,
    heatmap_data_copy: null,
    parallelsets_data_copy: null,
    priority_firewall: ['Info', 'Notice', 'Warning', 'Critical', 'Error'],
    priority_ids: ['3', '2', '1']

  },
  reducers: {
    setStackedBarchartData: (state, action) => {
      state.stackedbarchart_data = action.payload;
    },
    setStackedBarchartData_ids: (state, action) => {
      state.stackedbarchart_data_ids = action.payload;
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
      //console.log('action.payload', action.payload)
      state.priority_firewall = action.payload;
      //console.log('state.priority', state.priority_firewall)
    },
    filterPrioritiesIds: (state, action) => {
      console.log('action.payload', action.payload)
      state.priority_ids = action.payload;
      console.log('state.priority', state.priority_ids)
    }

  },

})

export const { filterPrioritiesFirewall, filterPrioritiesParallel, setStackedBarchartData, setHeatmapData, setParallelsetsData} = stateSlice.actions

export default stateSlice.reducer