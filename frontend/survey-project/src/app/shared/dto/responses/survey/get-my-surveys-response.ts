export interface SurveyDto {
    id: string;
    title: string;
    question: string;
    ending_time: string;
    user_ended: boolean;
    is_anonymous: boolean;
}

export interface GetMySurveysResponse {
    surveys?: SurveyDto[];
    status?: number;
    message?: string;
}