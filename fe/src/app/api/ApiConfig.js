const ENDPOINTS = {
    API_KEY: "AIzaSyCi8U3WDz3MUHr0YaL68UdCynQLqFtBl0M",
    PATHS:{
        BASE_PATH: "https://wade-rat-mihtei-rezciopan-crbqcods.ew.gateway.dev/",
        SPECIFICATIONS:{
            GET_ALL: "apis",
            SUBMIT_NEW_SPEC: "apis"
        },
        APINlp:{
            processNLP: (id)=> {return `apis/${id}/nlp-to-rest`;}
        },
        mockedApi:{
            mockGet: "http://dummy.restapiexample.com/api/v1/employees",
            mockedPost:
"https://wade-rat-mihtei-rezciopan-init-v2-crbqcods.ew.gateway.dev/apis?key=AIzaSyCi8U3WDz3MUHr0YaL68UdCynQLqFtBl0M"
        }
    }
};

export default ENDPOINTS;
