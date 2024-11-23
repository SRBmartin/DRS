import { Session } from "../../../model/user/session";

export interface RegisterResponse {
    message?: string;
    session?: Session;
}