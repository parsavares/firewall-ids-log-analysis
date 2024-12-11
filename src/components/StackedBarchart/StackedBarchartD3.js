import * as d3 from 'd3';


export default class StackedbarchartD3 {

    width;
    height;

    margin = {
    	top: 50,
    	right: 50,
    	bottom: 50,
    	left: 50
    };

    size;
    stackedbarSvg;
    x;
    y;
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

    updateAxis = function(){
        
        const bottomAxis = d3.axisBottom(this.x);
        const leftAxis = d3.axisLeft(this.y);

        this.stackedbarSvg.select(".xAxisG")
            .call(bottomAxis)            
            .selectAll("text")  
            .attr("transform", "rotate(-90)")
            //.attr("dy", "-0em")
            .attr("dx", "-5em")
        
        this.stackedbarSvg.select(".yAxisG")
            .call(leftAxis)
        ;

    }

    create = function(config){
        this.size = {width: config.size.width, height: config.size.height};
        // get the effect size of the view by subtracting the margin
        this.width = this.size.width - this.margin.left - this.margin.right;
        this.height = this.size.height - this.margin.top - this.margin.bottom;
        
        this.stackedbarSvg=d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class","stackedbarSvgG")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        ;
        // Build the axis
        this.stackedbarSvg.append("g")
            .attr("class","xAxisG")
            .attr("transform","translate(0,"+this.height+")");

        this.stackedbarSvg.append("g")
            .attr("class","yAxisG");

    }
    
    beBinnable = function(data){
        data.forEach(d => {
            d.date_time = new Date(d.date_time);
        });
    }


    render = function(data, xAttribute, yAttribute){ 

        console.assert(data.length>0, "data is empty");
        console.assert(xAttribute in data[0], "xAttribute not in data");
        console.assert(yAttribute in data[0], "yAttribute not in data");

        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;
        this.beBinnable(data);
        this.bin = d3.bin().value((d) => d.date_time).thresholds(this.numBins);

        const binned_data = this.bin(data)
        this.maxBins = d3.max(binned_data, d => d.length);
         console.log(this.maxBins)
        //this.updateAxis(data, xAttribute, yAttribute);
        this.timeExtent = d3.extent(data.map(d => d.date_time));

        this.x = d3.scaleTime().domain(this.timeExtent).range([this.margin.left, this.width - this.margin.right]);
        this.y = d3.scaleLinear().domain([0, this.maxBins]).nice().range([this.height - this.margin.bottom, this.margin.top])

    	
        //console.log("x:" , x);
        console.log("this.height", this.height);
        console.log("this.width", this.width);

        
    	
    	this.stackedbarSvg.attr("width", this.width).attr("height", this.height);
        
        
        this.updateAxis()
    	this.stackedbarSvg.append("g").selectAll("rect").data(binned_data).join("rect").attr("fill", "steelblue").attr("x", d => this.x(d.x0) + 1).attr("width", d => Math.max(0, this.x(d.x1) - this.x(d.x0) - 1)).attr("y", d => this.y(d.length)).attr("height", d => this.y(0) - this.y(d.length))




    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}