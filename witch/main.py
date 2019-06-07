from invoke import Collection, Program

from witch import VERSION
from .tasks import dev, prod, utils

namespace = Collection()
namespace.add_collection(prod)
namespace.add_collection(dev)
namespace.add_task(prod.deploy)
namespace.add_task(utils.collect_static)
namespace.add_task(utils.issue_certs)

program = Program(namespace=namespace, version=VERSION)
