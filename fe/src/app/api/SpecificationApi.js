import CallableApi from "./CallableApi";
import ENDPOINTS from "./ApiConfig";

const SpecificationApi = () =>{
    const getSpecifications = async() =>{
        return CallableApi().get(
            ENDPOINTS.PATHS.BASE_PATH + ENDPOINTS.PATHS.SPECIFICATIONS.GET_ALL
        );
    };
    const submitNewSpecification = async (resource) =>{
        return CallableApi().post(ENDPOINTS.PATHS.BASE_PATH + ENDPOINTS.PATHS.SPECIFICATIONS.SUBMIT_NEW_SPEC,
            null,

            resource);

    };
    return {
        getSpecifications,
        submitNewSpecification
    };

};


export default SpecificationApi;
