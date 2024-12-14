import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal } from 'd3-sankey';
import { syslog_priority_labels, syslog_priority_colors } from '../../utils';

export default class SankeyDiagramD3 {
    margin = { top: 20, right: 100, bottom: 20, left: 100 };
    size;
    height;
    width;
    SankeyDiagramSvg;
    sankeyGenerator;
    colorMap;

    constructor(el){
        this.el = el;
    }

    create = function(config){
        this.size = {width: config.size.width, height: config.size.height};
        // get the effect size of the view by subtracting the margin
        this.width = this.size.width - this.margin.left - this.margin.right;
        this.height = this.size.height - this.margin.top - this.margin.bottom;

        this.SankeyDiagramSvg = d3.select(this.el).append("svg")
            .attr("width", this.width + this.margin.left + this.margin.right)
            .attr("height", this.height + this.margin.top + this.margin.bottom)
            .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

        this.sankeyGenerator = sankey()
            .nodeWidth(15)
            .nodePadding(10)
            .extent([[1, 1], [this.width - 1, this.height - 5]]);

        this.colorMap = d3.scaleOrdinal()
            .domain(syslog_priority_labels)
            .range(syslog_priority_colors);
    }

    render = function(data) {

        const graph = this.transformData(data);
    

        // Create the sankey layout
        this.sankeyGenerator(graph);
    
        // Add links
        this.SankeyDiagramSvg.append("g")
            .selectAll(".link")
            .data(graph.links)
            .enter().append("path")
            .attr("class", "link")
            .attr("d", sankeyLinkHorizontal())
            .attr("stroke-width", d => Math.max(1, d.width))
            .style("stroke", d => {
                d.source.name = d.source.name.replace(/_0$/, '');
                if(syslog_priority_labels.includes(d.source.name)){
                    console.log(d.source.name)
                    return this.colorMap(d.source.name)
                }
                else
                    return "black";
            })
            //.style("fill", "none")
            .style("opacity", 0.5);
    
        // Add nodes (rectangles)
        var node = this.SankeyDiagramSvg.append("g")
            .selectAll(".node")
            .data(graph.nodes)
            .enter().append("g")
            .attr("class", "node")
            .attr("transform", function(d) { return "translate(" + d.x0 + "," + d.y0 + ")"; })

        node.append("rect")
                .attr("height", d => d.y1 - d.y0)
                .attr("width", this.sankeyGenerator.nodeWidth())
                //.style("fill", function(d) { return d.color = color(d.name.replace(/ .*/, "")); })
                .style("fill", d => {
                    d.name = d.name.replace(/_0$/, '');
                    if(syslog_priority_labels.includes(d.name)){
                        console.log(d)
                        return this.colorMap(d.name)
                    }
                    else{
                        return "black";
                    }
                })
                // Add hover text
                .append("title")
                .text(function(d) { return d.name + "\n" + "There is " + d.value + " stuff in this node"; });
        

        // add in the title for the nodes
        node.append("text")
            .attr("x", -6)
            .attr("y", function(d) { return (d.y1 - d.y0) / 2; })
            .attr("dy", ".35em")
            .attr("text-anchor", "end")
            .attr("transform", null)
            .text(function(d) { return d.name; })
        //.filter(function(d) { return d.x < width / 2; })
            .attr("x", 6 + this.sankeyGenerator.nodeWidth())
            .attr("text-anchor", "start");

    };

    transformData = function(data){


        


        const nodes = [];
        const links = [];

        data.forEach(d => {
            if (!nodes.some(n => n.name === d.source)) {
                nodes.push({ name: d.source });
            }
            if (!nodes.some(n => n.name === d.target)) {
                nodes.push({ name: d.target });
            }
            links.push({ source: d.source, target: d.target, value: d.value });
        });

        links.forEach(link => {
            link.source = nodes.findIndex(node => node.name === link.source);
            link.target = nodes.findIndex(node => node.name === link.target);
        });



        return { nodes, links };
    }

    clear = function(){
        d3.select(this.el).selectAll("*").remove();
    }
}
