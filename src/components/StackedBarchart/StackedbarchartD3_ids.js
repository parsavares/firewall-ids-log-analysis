import * as d3 from 'd3';


export default class StackedbarchartD3_ids {

    width;
    height;

    margin = {
    	top: 10,
    	right: 50,
    	bottom: 200,
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
        .range([this.margin.left, this.width - this.margin.right])
        .padding(0.1);

        this.y = d3.scaleLinear()
        .domain([0, maxBar])
        .rangeRound([this.height - this.margin.bottom, this.margin.top]);

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
            .attr("transform","translate(0," + (this.height + this.margin.top) + ")");

        this.stackedbarSvg.append("g")
            .attr("class","yAxisG");

    }
    
    render = function(data, xAttribute, yAttribute){ 

        
        this.visData = data;
        this.xAttribute = xAttribute;
        this.yAttribute = yAttribute;

        d3.select(".seriesG").remove()
        
        this.stackedbarSvg.append("g")
        const subgroups = Object.keys(data[0].occurrences); 

        console.log("sub: ", subgroups)

        this.updateAxis(data)

        const colorMap = d3.scaleOrdinal()
        .domain(subgroups)
        .range(d3.schemeCategory10)
        //console.log('color_map', colorMap)


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
        .attr("class", "seriesG")
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
    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}