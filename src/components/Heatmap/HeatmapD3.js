import * as d3 from 'd3';
import mock_data from './heatmap_data.csv';
import generateMockData from './generate_data';


export default class HeatmapD3 {
    margin = { top: 100, right: 50, bottom: 100, left: 50 };
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

    
        var myGroups = Array.from(new Set(visData.map(d => d.xAttribute)));
        var myVars = Array.from(new Set(visData.map(d => d.yAttribute)));


        this.xScale = d3.scaleBand()
        .range([ 0, this.width ])
        .domain(myGroups)
        .padding(0.05);

        this.yScale = d3.scaleBand()
        .range([ this.height, 0 ])
        .domain(myVars)
        .padding(0.05);

        const bottomAxis = d3.axisBottom(this.xScale);
        const leftAxis = d3.axisLeft(this.yScale);

        this.heatmapSvg.select(".xAxisG")
            .transition().duration(this.transitionDuration)
            .call(bottomAxis)            
            .selectAll("text")  
            .attr("transform", "rotate(-65)");
        
        this.heatmapSvg.select(".yAxisG")
            .transition().duration(this.transitionDuration)
            .call(leftAxis)
        ;
 
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

        // Build the axis
        this.heatmapSvg.append("g")
            .attr("class","xAxisG")
            .attr("transform","translate(0,"+this.height+")");

        this.heatmapSvg.append("g")
            .attr("class","yAxisG");
        

    }

   render = function(data, xAttribute, yAttribute){ 


        console.log(data);  
        console.log(xAttribute);
        console.log(yAttribute);

        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;

        this.updateAxis(data, xAttribute, yAttribute);

        var maxFrequency = d3.max(data, d => d.frequency);
        var myColor = d3.scaleSequential()
        .interpolator(d3.interpolateViridis)
        .domain([1, maxFrequency])

        this.heatmapSvg.selectAll(".squareG")
        .data(data, function(d) {return d.xAttribute+':'+d.yAttribute;})
        .enter()
        .append("rect")
            .attr("x", (d) => { return this.xScale(d.xAttribute) })
            .attr("y", (d) => { return this.yScale(d.yAttribute) })
            .attr("rx", 4)
            .attr("ry", 4)
            .attr("width", this.xScale.bandwidth() )
            .attr("height", this.yScale.bandwidth() )
            .style("fill", function(d) { return myColor(d.frequency)} )
            .style("stroke-width", 4)
            .style("stroke", "none")
            .style("opacity", 0.8)  

    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}