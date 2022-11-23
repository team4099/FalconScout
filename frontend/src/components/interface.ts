export interface ComponentSetup {
    text?: string;
    route?: string;
    options?: Array<string>;
    placeholder?: Array<string>;
}

export interface PageSetup {
    config?: object // TODO: find the proper type
}