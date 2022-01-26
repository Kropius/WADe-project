import CallableApi from "./CallableApi";
import ENDPOINTS from "./ApiConfig";

const SpecificationApi = () =>{
    const getSpecifications = async() =>{
        return CallableApi().get(
            ENDPOINTS.PATHS.mockedApi.mockGet
        );
    };
    return {
        getSpecifications
    };

};


export default SpecificationApi;
