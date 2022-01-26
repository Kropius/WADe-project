import CallableApi from "./CallableApi";
import ENDPOINTS from "./ApiConfig";

const NLPApi = () =>{
    const processNLP = async(resource, specId) =>{
        return CallableApi().post(ENDPOINTS.PATHS.BASE_PATH + ENDPOINTS.PATHS.APINlp.processNLP(specId),
            resource, {key: ENDPOINTS.API_KEY});
    };

    const mockPost = async() =>{
        return CallableApi().post(ENDPOINTS.PATHS.mockedApi.mockedPost);
    };
    return {
        processNLP,
        mockPost
    };
};

export default NLPApi;
