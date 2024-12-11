import * as d3 from 'd3';


export default class StackedbarchartD3 {
    viewSize = {
    	width: 1200,
    	height: 600
    };
    margin = {
    	top: 5,
    	right: 10,
    	bottom: 5,
    	left: 10
    };
    //width = 960;
    //height = 500;
    marginTop = 20;
    marginRight = 20;
    marginBottom = 30;
    marginLeft = 40;
    size;
    height;
    width;
    chartSVG;
    xScale;
    yScale;
    visData;
    xAttribute;
    yAttribute;
    controllerMethods;
    numBins = 40;
    maxBins;
    bin;
    timeExtent = [new Date(), new Date(0)];

    
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
        
        this.chartSVG=d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class","heatmapSvgG")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        ;


    }
    
    beBinnable = function(data){
        data.forEach(d => {
            d.Date_time = new Date(d.Date_time);
        });
    }

    createBins = function(data){
        this.bin = d3.bin().value((d) => d.Date_time).thresholds(this.numBins);
    }
    render = function(data, xAttribute, yAttribute){ 

        console.assert(data.length>0, "data is empty");
        console.assert(xAttribute in data[0], "xAttribute not in data");
        console.assert(yAttribute in data[0], "yAttribute not in data");

        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;
        this.beBinnable(data);
        this.createBins(data);

        //this.updateAxis(data, xAttribute, yAttribute);
        this.timeExtent = d3.extent(data.map(x => x.Date_time));
        this.maxBins = d3.max(data, d => d.length);
    	const x = d3.scaleTime().domain(this.timeExtent).range([this.margin.left, this.width - this.margin.right]);
    	const y = d3.scaleLinear().domain([0, d3.max(data, d => d.length)]).nice().range([this.height - this.margin.bottom, this.margin.top]),
    		xAxis = g => g.attr("transform", `translate(0,${this.height - this.margin.bottom})`).call(d3.axisBottom(x).tickSizeOuter(0)).call(g => g.append("text").attr("x", this.width / 2).attr("y", 30).attr("fill", "#000").attr("font-weight", "bold").attr("text-anchor", "end").text("Time of Event"));
    	this.chartSVG.attr("width", this.chartWidth).attr("height", this.chartHeight);
    	this.chartSVG.append("g").selectAll("rect").data(data).join("rect").attr("fill", "steelblue").attr("x", d => x(d.x0) + 1).attr("width", d => Math.max(0, x(d.x1) - x(d.x0) - 1)).attr("y", d => y(d.length)).attr("height", d => y(0) - y(d.length))

    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}