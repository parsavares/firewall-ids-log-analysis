import { configureStore } from '@reduxjs/toolkit'
import stateReducer from './redux/DatasetSlice'
export default configureStore({
  reducer: {
    state: stateReducer,
    }
})