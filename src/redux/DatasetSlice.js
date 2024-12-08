import { createSlice, createAsyncThunk } from '@reduxjs/toolkit'
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

const prepareInitialState = (data) => {


  return {
    xAttribute: "FirstValue",
    yAttribute: "SecondValue",
    data: [] 
  }
}

export const stateSlice = createSlice({
  name: 'state',
  initialState: {
    xAttribute: "FirstValue",
    yAttribute: "SecondValue",
    data: [] 
  },
  reducers: {},
  extraReducers: builder => {
    builder.addCase(fetchFileData.fulfilled, (state, action) => {
      // Add any fetched house to the array
      return prepareInitialState(action.payload)
    })
  }
})

// Action creators are generated for each case reducer function
export const {  updateAxisAttributes, updateSelectedItemsIndices} = stateSlice.actions

export default stateSlice.reducer