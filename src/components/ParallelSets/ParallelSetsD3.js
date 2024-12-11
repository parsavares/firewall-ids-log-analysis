import * as d3 from 'd3';


export default class ParallelSetsD3 {
    margin = { top: 100, right: 100, bottom: 10, left: 100 };
    size;
    height;
    width;
    parallelSetsSvg;
    xScale;
    yScales;
    visData;
    xAttribute;
    yAttribute;
    controllerMethods;
    path;
    dimensions;

    constructor(el){
        this.el = el;
    }

    updateAxis = function(visData){

        this.dimensions = Object.keys(visData[0])
        this.yScales = {}
        for (let i in this.dimensions) {
            const name = this.dimensions[i]
            //const domain = d3.extent(visData, function(d) { return d[name]; })
            const domain = [...new Set(visData.map(d => d[name]))]
            console.log(domain)
            this.yScales[name] = d3.scalePoint()
            .domain(domain)
            .range([this.height, 0])
        }

        this.xScale = d3.scalePoint()
        .range([0, this.width])
        .padding(1)
        .domain(this.dimensions);

        this.path = (d) => {
            return d3.line()(this.dimensions.map((p) => { return [this.xScale(p), this.yScales[p](d[p])]; }));
        }

        this.parallelSetsSvg.selectAll("myAxis")
        // For each dimension of the dataset I add a 'g' element:
        .data(this.dimensions).enter()
        .append("g")
        // I translate this element to its right position on the x axis
        .attr("transform", (d) => { return "translate(" + this.xScale(d) + ")"; })
        // And I build the axis with the call function
        .each((d, i, nodes) => {
            return d3.select(nodes[i]).call(d3.axisLeft().scale(this.yScales[d]));
        })
        // Add axis title
        .append("text")
          .style("text-anchor", "middle")
          .attr("y", -9)
          .text(function(d) { return d; })
          .style("fill", "black")

    }

    create = function(config){
        this.size = {width: config.size.width, height: config.size.height};
        // get the effect size of the view by subtracting the margin
        this.width = this.size.width - this.margin.left - this.margin.right;
        this.height = this.size.height - this.margin.top - this.margin.bottom;

        this.parallelSetsSvg=d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .append("g")
            .attr("class","parallelSetsSvgG")
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");
        ;


    }

   render = function(data){ 


        this.visData = data;

        this.updateAxis(data);
        console.log(this.yScales)

        const firstAttribute = this.dimensions[0];
        const uniqueValues = [...new Set(data.map(d => d[firstAttribute]))];

        const colorMap = d3.scaleOrdinal()
            .domain(uniqueValues)
            .range(d3.schemeCategory10)



        this.parallelSetsSvg
        .selectAll("myPath")
        .data(data)
        .enter().append("path")
        .attr("d",  this.path)
        .style("fill", "none")
        .style("stroke", d => colorMap(d[firstAttribute]))
        .style("opacity", 1)
        .style("stroke-width", 0.5)

    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}