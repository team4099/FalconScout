export interface ComponentSetup {
    text?: string;
    route?: string;
    options?: Array<string>;
    placeholder?: Array<string>;
    getValue?: any;
    setValue?: any;
    id?: any;
    required?: any
}

export interface PageSetup {
    config?: any // TODO: find the proper type
}