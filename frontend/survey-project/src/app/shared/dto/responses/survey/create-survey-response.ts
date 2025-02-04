import { Survey } from "../../../model/survey/Survey";

export interface CreateSurveyResponse{
    status?: string;
    message?: string;
    survey?: Survey;
};