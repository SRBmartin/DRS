import { Survey } from "../../../model/survey/Survey";

export interface SurveyDetailsResponse {
    status?: number;
    message?: string;
    data?: Survey;
}
