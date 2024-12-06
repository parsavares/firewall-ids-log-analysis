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

    
        var myGroups = Array.from(new Set(visData.map(d => d.sourceIp)));
        var myVars = Array.from(new Set(visData.map(d => d.destinationIp)));


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

        //d3.csv(mock_data).then((fetched_data) => {

            var fetched_data = generateMockData();
            this.xAttribute = xAttribute;
            this.yAttribute = yAttribute;
            this.visData = fetched_data;
            console.log(fetched_data);

            this.updateAxis(fetched_data, xAttribute, yAttribute);

            var myColor = d3.scaleSequential()
            .interpolator(d3.interpolateInferno)
            .domain([1,100])

            this.heatmapSvg.selectAll(".squareG")
            .data(fetched_data, function(d) {return d.sourceIp+':'+d.destinationIp;})
            .enter()
            .append("rect")
              .attr("x", (d) => { return this.xScale(d.sourceIp) })
              .attr("y", (d) => { return this.yScale(d.destinationIp) })
              .attr("rx", 4)
              .attr("ry", 4)
              .attr("width", this.xScale.bandwidth() )
              .attr("height", this.yScale.bandwidth() )
              .style("fill", function(d) { return myColor(d.frequency)} )
              .style("stroke-width", 4)
              .style("stroke", "none")
              .style("opacity", 0.8)
        
        //})

        
   }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}