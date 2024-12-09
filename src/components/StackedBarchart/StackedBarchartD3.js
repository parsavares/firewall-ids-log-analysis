import * as d3 from 'd3';


export default class StackedbarchartD3 {
    margin = { top: 100, right: 100, bottom: 100, left: 100 };
    size;
    height;
    width;
    heatmapSvg;
    xScale;
    yScale;
    visData;
    xAttribute;
    yAttribute;
    controllerMethods;
    
    constructor(el){
        this.el = el;
    }

    updateAxis = function(visData,xAttribute,yAttribute){
 
    }

    create = function(config){
        this.size = {width: config.size.width, height: config.size.height};
        // get the effect size of the view by subtracting the margin
        this.width = this.size.width - this.margin.left - this.margin.right;
        this.height = this.size.height - this.margin.top - this.margin.bottom;

        this.heatmapSvg=d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class","heatmapSvgG")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        ;


    }

   render = function(data, xAttribute, yAttribute){ 

        console.assert(data.length>0, "data is empty");
        console.assert(xAttribute in data[0], "xAttribute not in data");
        console.assert(yAttribute in data[0], "yAttribute not in data");

        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;

        this.updateAxis(data, xAttribute, yAttribute);

    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}