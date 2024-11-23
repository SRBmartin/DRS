import { Session } from "../../../model/user/session";

export interface LoginResponse {
    message?: string;
    session?: Session;
}