counts = {}
total = 0

def incrementEndpointCallCount(endpoint, method):
    global counts
    
    if endpoint in counts:
        if method in counts[endpoint]:
            counts[endpoint][method] += 1
        else:
            counts[endpoint][method] = 1
    else:
        counts[endpoint] = {method : 1}
     
    global total
    for k in counts:
        if k != "total":
            for v in counts[k]:
                total += counts[k][v]

    counts["total"] = total
