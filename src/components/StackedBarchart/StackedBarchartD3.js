import * as d3 from 'd3';
import { syslog_priority_colors, syslog_priority_labels} from '../../utils'

export default class StackedbarchartD3 {

    width;
    height;

    margin = {
    	top: 10,
    	right: 200,
    	bottom: 200,
    	left: 200
    };

    size;
    stackedbarSvg;
    x;
    y;
    visData;
    xAttribute;
    yAttribute;
    controllerMethods;

    
    constructor(el){
        this.el = el;
    }

    updateAxis = function(data){
        
        const groups = data.map(d => d.interval_center)
        const maxBar = d3.max(d3.map(data, g => g.total_occurrences)) 

        console.log("groups: ", groups)
        console.log("maxBar: ", maxBar)
        // Prepare the scales for positional and color encodings.
        this.x = d3.scaleBand()
        .domain(groups)
        .range([0, this.width])
        .padding(0.1);

        this.y = d3.scaleLinear()
        .domain([0, maxBar])
        .rangeRound([this.height, 0])

        const bottomAxis = d3.axisBottom(this.x).tickValues(this.x.domain().filter(function(d,i){ return !(i%10)}));

        const leftAxis = d3.axisLeft(this.y);

        this.stackedbarSvg.select(".xAxisG")
            .call(bottomAxis)            
            .selectAll("text")  
            .attr("transform", "rotate(-90)")
            .attr("dy", "-0em")
            .attr("dx", "-10em")

        
        this.stackedbarSvg.select(".yAxisG")
            .call(leftAxis)
        ;

    }

    create = function(config){
        this.size = {width: config.size.width, height: config.size.height};
        // get the effect size of the view by subtracting the margin
        this.width = this.size.width - this.margin.left - this.margin.right;
        this.height = this.size.height - this.margin.top - this.margin.bottom;
        
        // Ensure tooltip element exists
        if (d3.select("#tooltip").empty()) {
            d3.select("body").append("div")
                .attr("id", "tooltip")
                .style("position", "absolute")
                .style("display", "none")
                .style("border-radius", "5px")
                .style("position", "absolute")
                .style("background-color", "white")
                .style("border", "solid")
                .style("border-width", "1px")
                    .style("padding", "10px");
        }
                // Create a tooltip div. This should be added to your HTML file or dynamically created in your script.
                if (d3.select(this.el).select(".tooltip").empty()) {
                    d3.select(this.el).append("div")
                    .attr("class", "tooltip")
                    .style("opacity", 0)
                    .style("position", "absolute")
                    .style("background-color", "white")
                    .style("border", "solid")
                    .style("border-width", "1px")
                        .style("padding", "10px");
                    }

        this.stackedbarSvg = d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class","stackedbarSvgG")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        ;
        // Build the axis
        this.stackedbarSvg.append("g")
            .attr("class","xAxisG")
            .attr("transform","translate(0," + (this.height + this.margin.top) + ")");

        this.stackedbarSvg.append("g")
            .attr("class","yAxisG");

    }
    
    render = function(data, xAttribute, yAttribute){ 

        
        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;

        
        const subgroups = Object.keys(data[0].occurrences); 

        console.log("sub: ", subgroups)

        this.updateAxis(data)

        const colorMap = d3.scaleOrdinal()
        .domain(syslog_priority_labels)
        .range(syslog_priority_colors);


        // Prepare the data for the stack layout
        let data_to_stack = [];
        data.forEach(d => {
            let mergedOccurrences = {};
            subgroups.forEach(subgroup => {
                mergedOccurrences[subgroup] = d.occurrences[subgroup];
            });
            data_to_stack.push({
                interval_center: d.interval_center,
                ...mergedOccurrences
            });
        });
            
        const stackedData = d3.stack()
        .keys(subgroups)
        (data_to_stack)

        console.log("stacked data: ", stackedData)

        // Append a group for each series, and a rect for each element in the series.
        this.stackedbarSvg.append("g")
        .selectAll("g")
        // Enter in the stack data = loop key per key = group per group
        .data(stackedData)
        .enter().append("g")
          .attr("fill", d => colorMap(d.key) )
          .selectAll("rect")
          // enter a second time = loop subgroup per subgroup to add all rectangles
          .data(function(d) { return d; })
          .enter().append("rect")
            .attr("x", d =>  this.x(d.data.interval_center))
            .attr("y", d =>  this.y(d[1])) 
            .attr("height", d => this.y(d[0]) - this.y(d[1]))
            .attr("width", this.x.bandwidth())
            .on("mouseover", (event, d) => {
                const [x, y] = d3.pointer(event);
                const categoryData = `Interval Center: ${d.data.interval_center}<br>` + subgroups.map(subgroup => `${subgroup}: ${d.data[subgroup]}`).join("<br>");
                d3.select("#tooltip")
                    .style("left", `${x + 10}px`)
                    .style("top", `${y + 10}px`)
                    .style("display", "inline-block")
                    .html(categoryData);
            })
            .on("mouseout", function() {
            d3.select("#tooltip")
                .style("display", "none");
            })
            
    }
    

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}