import {
    SIGNUP_SUCCESS,
    SIGNUP_FAIL,
    LOGIN_SUCCESS,
    LOGIN_FAIL,
    LOGOUT,
    FORGET_USER
} from '../action/types';

const initialState = {
    token: localStorage.getItem('token'),
    idUser: localStorage.getItem('iduser'),
    email: localStorage.getItem('email'),
    avatar: localStorage.getItem('avatar'),
    username: localStorage.getItem('username')
};

export default function(state = initialState, action) {
    const { type, payload } = action;

    switch(type) {
        case LOGIN_SUCCESS:
            localStorage.setItem('token', payload.token.refresh);
            localStorage.setItem('iduser', payload.id);
            localStorage.setItem('email', payload.email);
            localStorage.setItem('avatar', payload.avatar);
            localStorage.setItem('username', payload.username);
            return {
                ...state,
                token: payload.token.access,
                idUser: payload.id,
                email: payload.email,
                avatar: payload.avatar,
                username: payload.username
            }
        case SIGNUP_SUCCESS:
            localStorage.setItem('token', payload.token.refresh);
            localStorage.setItem('iduser', payload.id);
            localStorage.setItem('email', payload.email);
            localStorage.setItem('avatar', payload.avatar);
            localStorage.setItem('username', payload.username);
            return {
                ...state,
                token: payload.token.access,
                idUser: payload.id,
                email: payload.email,
                avatar: payload.avatar,
                username: payload.username
            }
        case SIGNUP_FAIL:
        case LOGIN_FAIL:
        case LOGOUT:
            localStorage.removeItem('token');
            localStorage.removeItem('iduser');
            localStorage.removeItem('email');
            localStorage.removeItem('avatar');
            localStorage.removeItem('username');
            return {
                ...state,
                token: null,
                idUser: null,
                email: null,
                avatar: null,
                username: null
            }
        case FORGET_USER:
        default:
            return state
    }
}